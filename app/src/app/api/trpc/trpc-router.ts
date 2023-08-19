import { initTRPC } from "@trpc/server";
import superjson from "superjson";

const t = initTRPC.create({
  transformer: superjson,
});

export const appRouter = t.router({
  hello: t.procedure.query(({ ctx }) => {
    return "Hello and welcome!";
  }),
});

export type AppRouter = typeof appRouter;