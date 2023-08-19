import { appRouter } from "../api/trpc/trpc-router";

/** This is a React Server Component */
export default async function RSCPage() {
    const caller = appRouter.createCaller({});
    // call the tRPC endpoint
    const message = await caller.hello();

    // we render this output on the server
    return  (
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
          <div className="shadow-xl">{message}</div>
        </div>
      </main>
    )
}