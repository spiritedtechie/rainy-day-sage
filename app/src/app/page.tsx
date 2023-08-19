"use client";

import Image from 'next/image'
import { trpc } from "@/utils/trpc";

export default function Home() {
  let { data: message, isLoading, isFetching } = trpc.hello.useQuery();

  if (isLoading || isFetching) {
    return <p>Loading...</p>;
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <div className="shadow-xl">{message}</div>
      </div>
    </main>
  )
}
