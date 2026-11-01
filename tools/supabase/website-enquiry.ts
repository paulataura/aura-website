// Receives enquiries from the aurasolutions.co.uk contact form.
// Saves them to public.website_enquiries and, when SMTP secrets are set,
// emails the team. No login needed: it validates, rate-limits and uses a honeypot.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.45.4";
import nodemailer from "npm:nodemailer@6.9.14";

const ALLOWED = ["https://aurasolutions.co.uk", "https://www.aurasolutions.co.uk", "http://localhost:8765"];

function cors(origin: string | null) {
  const o = origin && ALLOWED.includes(origin) ? origin : ALLOWED[0];
  return {
    "Access-Control-Allow-Origin": o,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Vary": "Origin",
  };
}

const clip = (v: unknown, n: number) => {
  const s = typeof v === "string" ? v.trim() : "";
  return s ? s.slice(0, n) : null;
};

async function sha256(s: string) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

const esc = (s: string | null) => (s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));

Deno.serve(async (req) => {
  const headers = { ...cors(req.headers.get("origin")), "Content-Type": "application/json" };
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers });
  if (req.method !== "POST") return new Response(JSON.stringify({ ok: false }), { status: 405, headers });

  let body: Record<string, unknown>;
  try { body = await req.json(); } catch { return new Response(JSON.stringify({ ok: false, error: "bad_request" }), { status: 400, headers }); }

  // Honeypot and timing: bots fill hidden fields or submit instantly. Pretend success.
  const elapsed = Number(body.elapsed_ms ?? 0);
  if (clip(body.website, 200) || elapsed < 2500) return new Response(JSON.stringify({ ok: true }), { headers });

  const rec = {
    name: clip(body.name, 120),
    phone: clip(body.phone, 40),
    email: clip(body.email, 200),
    postcode: clip(body.postcode, 12)?.toUpperCase() ?? null,
    service: clip(body.service, 120),
    urgency: clip(body.urgency, 60),
    message: clip(body.message, 4000),
    source_page: clip(body.source_page, 300),
  };
  if (!rec.name || !rec.phone || rec.phone.replace(/\D/g, "").length < 7) {
    return new Response(JSON.stringify({ ok: false, error: "missing_fields" }), { status: 422, headers });
  }
  if (rec.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(rec.email)) rec.email = null;

  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
  const ip = (req.headers.get("x-forwarded-for") ?? "").split(",")[0].trim();
  const ip_hash = ip ? await sha256(ip + "aura-enquiry") : null;

  if (ip_hash) {
    const since = new Date(Date.now() - 10 * 60 * 1000).toISOString();
    const { count } = await db.from("website_enquiries").select("id", { count: "exact", head: true }).eq("ip_hash", ip_hash).gte("created_at", since);
    if ((count ?? 0) >= 5) return new Response(JSON.stringify({ ok: false, error: "too_many" }), { status: 429, headers });
  }

  const { data, error } = await db.from("website_enquiries").insert({ ...rec, ip_hash }).select("id").single();
  if (error) {
    console.error("insert failed", error.message);
    return new Response(JSON.stringify({ ok: false, error: "save_failed" }), { status: 500, headers });
  }

  // Email the team if SMTP is configured (secrets SMTP_HOST, SMTP_USER, SMTP_PASS; optional SMTP_PORT, ENQUIRY_TO).
  const host = Deno.env.get("SMTP_HOST"), user = Deno.env.get("SMTP_USER"), pass = Deno.env.get("SMTP_PASS");
  if (host && user && pass) {
    try {
      const port = Number(Deno.env.get("SMTP_PORT") ?? 465);
      const t = nodemailer.createTransport({ host, port, secure: port === 465, auth: { user, pass } });
      // "Tank cleaning page (/tank-cleaning.html)" -> "Tank cleaning"
      const pageName = rec.source_page?.replace(/ page \(.*\)$/, "") ?? "Website";
      const service = rec.service ?? "Not specified";
      const rows = [["Page", rec.source_page], ["Service", service], ["Urgency", rec.urgency], ["Name", rec.name], ["Phone", rec.phone], ["Email", rec.email], ["Site postcode", rec.postcode]];
      await t.sendMail({
        from: `"Aura website" <${user}>`,
        to: Deno.env.get("ENQUIRY_TO") ?? user,
        replyTo: rec.email ?? undefined,
        subject: `${rec.urgency?.startsWith("Emergency") ? "URGENT " : ""}Website enquiry: ${service} (from ${pageName} page) - ${rec.name}`,
        text: rows.map(([k, v]) => `${k}: ${v ?? "-"}`).join("\n") + `\n\n${rec.message ?? ""}`,
        html: `<table cellpadding="4">${rows.map(([k, v]) => `<tr><td><b>${k}</b></td><td>${esc(v)}</td></tr>`).join("")}</table><p>${esc(rec.message).replace(/\n/g, "<br>")}</p>`,
      });
    } catch (e) {
      console.error("email failed", (e as Error).message);
    }
  }

  return new Response(JSON.stringify({ ok: true, id: data.id }), { headers });
});
