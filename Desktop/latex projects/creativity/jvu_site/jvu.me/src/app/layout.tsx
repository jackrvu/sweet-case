import './globals.css'
import { Azeret_Mono } from 'next/font/google'

const mono = Azeret_Mono({
  weight: ['200', '600'],
  subsets: ['latin'],
  display: 'swap',
})

export const metadata = {
  title: 'jackrvu',
  description: 'status, links, visitors, about me, posts',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${mono.className} bg-dark-blue bg-dot-pattern bg-dot-pattern min-h-screen flex justify-center`}>
        <div className="bg-white w-full h-full p-4 flex flex-col mt-12 custom-width"> 
          {children}
        </div>
      </body>
    </html>
  )
}