"use client";

import { trpc } from "@/utils/trpc";

export default function Home() {
  let { data: message, isLoading, isFetching } = trpc.hello.useQuery();

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <div className="shadow-xl">{(isLoading || isFetching) ? "Loading..." : message}</div>
      </div>
    </main>
  )
}
