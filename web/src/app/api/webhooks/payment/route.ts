import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import crypto from 'crypto';

// Generate a license key: SNAG-XXXX-XXXX-XXXX
function generateLicenseKey() {
  const segment = () => crypto.randomBytes(2).toString('hex').toUpperCase();
  return `SNAG-${segment()}-${segment()}-${segment()}`;
}

export async function POST(req: Request) {
  try {
    const payload = await req.json();
    
    // 1. Verify webhook signature (omitted for brevity, implement based on Razorpay/PayPal docs)
    // 2. Parse the plan from the payload
    const plan_type = payload.plan_type || 'lifetime';
    
    // 3. Generate key
    const license_key = generateLicenseKey();
    
    // 4. Calculate expiration
    let expires_at = null;
    if (plan_type === 'monthly') {
      const d = new Date();
      d.setMonth(d.getMonth() + 1);
      expires_at = d.toISOString();
    } else if (plan_type === 'yearly') {
      const d = new Date();
      d.setFullYear(d.getFullYear() + 1);
      expires_at = d.toISOString();
    }
    
    // 5. Insert into DB
    const { error } = await supabase.from('licenses').insert([
      {
        license_key,
        plan_type,
        is_active: true,
        expires_at
      }
    ]);

    if (error) {
      console.error("Supabase insert error:", error);
      return NextResponse.json({ error: 'Database error' }, { status: 500 });
    }

    // 6. Return the key (or send via email)
    return NextResponse.json({ success: true, license_key }, { status: 200 });

  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
