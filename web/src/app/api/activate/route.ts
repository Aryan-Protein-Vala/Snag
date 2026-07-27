import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

export async function POST(req: Request) {
  try {
    const { license_key, device_id } = await req.json();

    if (!license_key || !device_id) {
      return NextResponse.json({ error: 'Missing license_key or device_id' }, { status: 400 });
    }

    // Super Admin Bypass
    if (license_key === 'SNAG-SUPER-ADMIN') {
      return NextResponse.json({ success: true, message: 'Super Admin activated successfully.' }, { status: 200 });
    }

    // 1. Fetch the license
    const { data: license, error } = await supabase
      .from('licenses')
      .select('*')
      .eq('license_key', license_key)
      .single();

    if (error || !license) {
      return NextResponse.json({ error: 'Invalid license key' }, { status: 404 });
    }

    if (!license.is_active) {
      return NextResponse.json({ error: 'License is inactive' }, { status: 403 });
    }

    // 2. Check device ID
    if (!license.device_id) {
      // First time activation - bind device
      const { error: updateError } = await supabase
        .from('licenses')
        .update({ device_id: device_id })
        .eq('id', license.id);

      if (updateError) {
        return NextResponse.json({ error: 'Failed to bind device' }, { status: 500 });
      }

      return NextResponse.json({ success: true, message: 'License activated successfully.' }, { status: 200 });
    }

    if (license.device_id === device_id) {
      // Already activated on this device
      return NextResponse.json({ success: true, message: 'License verified.' }, { status: 200 });
    } else {
      // Activated on another device
      return NextResponse.json({ error: 'License already activated on another device.' }, { status: 403 });
    }

  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
