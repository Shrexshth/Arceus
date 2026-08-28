import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const { tableName, rowCount } = await req.json();

    if (!tableName || !rowCount) {
      return NextResponse.json({ error: 'Missing table name or row count' }, { status: 400 });
    }

    if (tableName !== 'users') {
      return NextResponse.json({ error: `Table '${tableName}' does not exist.` }, { status: 400 });
    }

    // Mock data generation for hackathon since TrueForge agent API is stubbed
    const data = [];
    const timestamp = Date.now();
    for (let i = 1; i <= rowCount; i++) {
      data.push({
        name: `Generated User ${i}`,
        email: `user${timestamp}_${i}@example.com`,
        created_at: new Date().toISOString()
      });
    }

    return NextResponse.json({ data });
  } catch (error) {
    console.error('Error generating data:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
