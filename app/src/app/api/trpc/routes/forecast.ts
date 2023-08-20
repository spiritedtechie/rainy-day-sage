import { TRPCError } from '@trpc/server';
import { router, publicProcedure } from '../trpc';


type Forecast = {
  summary: string;
	status: string;
  'inspiring-message': string
}

const fetchForecast = async () => {
  return await fetch('http://127.0.0.1:3001',{cache: "no-cache"})
    .then(res => res.json())
    .then(res => {
      return res as Forecast
    })
}

export const forecastRouter = router({
  get: publicProcedure.query(async () => {
    
    try {
      return await fetchForecast()
    } catch(e){
      throw new TRPCError({
        code: 'INTERNAL_SERVER_ERROR',
        message: 'Unable to fetch forecast data.',
        cause: e,
      });
    }
  }),
});