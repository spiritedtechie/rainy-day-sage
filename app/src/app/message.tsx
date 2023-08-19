"use client";

import { trpc } from "@/utils/trpc";

export default function Message() {

  let { data: message, isLoading, isFetching } = trpc.hello.useQuery();

  return (
    <div className="shadow-xl">{(isLoading || isFetching) ? "Loading..." : message}</div>
  )
}
