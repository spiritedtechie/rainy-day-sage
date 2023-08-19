import {forecastRouter} from "./routes/forecast"
import {router} from "../trpc/trpc"

export const appRouter = router({
  forecast: forecastRouter
});
 

export type AppRouter = typeof appRouter;