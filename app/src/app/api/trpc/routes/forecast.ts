import { router, publicProcedure } from '../trpc';


type Forecast = {
  summary: string;
	status: string;
  'inspiring-message': string
}

const fetchForecast = async () => {
  return await fetch('http://127.0.0.1:3001')
    .then(res => res.json())
    .then(res => {
      return res as Forecast
    })
}

export const forecastRouter = router({
  get: publicProcedure.query(async () => {
    const result = await fetchForecast()
    return result;
  }),
});