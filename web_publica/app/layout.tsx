import type { Metadata } from "next";
export const metadata: Metadata = {title:"Observatorio Retail · Agente BI",description:"Ventas reales, herramientas MCP y Supabase. Auditoría, acciones propuestas y escenarios explícitos."};
export default function RootLayout({children}: {children:React.ReactNode}) {return <html lang="es"><body>{children}</body></html>}
