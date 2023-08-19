"use client";

import { trpc } from "@/utils/trpc";

export default function Message() {
  let { data: message, isLoading, isFetching } = trpc.hello.useQuery();

  return (
    <div className="animate-typing overflow-hidden whitespace-nowrap border-r-4 border-r-white pr-5 text-5xl text-white font-bold">
      {isLoading || isFetching ? "" : message}
    </div>
  );
}
