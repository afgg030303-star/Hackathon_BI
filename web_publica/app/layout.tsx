import type { Metadata } from "next";
export const metadata: Metadata = {title:"Observatorio Retail · Agente BI",description:"Ventas reales, herramientas MCP y Supabase. Agente local sin API de pago."};
export default function RootLayout({children}: {children:React.ReactNode}) {return <html lang="es"><body>{children}</body></html>}
