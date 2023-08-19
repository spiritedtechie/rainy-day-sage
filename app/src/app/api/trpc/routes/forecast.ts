import { router, publicProcedure } from '../trpc';

export const forecastRouter = router({
  get: publicProcedure.query(() => {
    return "Hello and welcome!";
  }),
});