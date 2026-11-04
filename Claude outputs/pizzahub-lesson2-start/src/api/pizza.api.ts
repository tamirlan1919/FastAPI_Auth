// Слой API. Отвечает за: получить пиццы с «сервера» и отдать приложению в НАШЕМ формате.
import type { Pizza } from '../types';
import { withCache, withLogging, withRetry } from '../lib/decorators';
import { getPizzasFromServer } from './fake-backend';
import { toPizza } from './pizza.adapter';

// Шаг Adapter: просто загрузка + перевод формата
export async function fetchPizzas(): Promise<Pizza[]> {
  const raw = await getPizzasFromServer();
  return raw.map(toPizza);
}

// Шаг Decorator: та же функция в трёх обёртках
export const getMenu = withLogging(withCache(withRetry(fetchPizzas), 60_000), 'getMenu');
