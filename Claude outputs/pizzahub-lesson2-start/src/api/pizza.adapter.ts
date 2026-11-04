// ADAPTER. Отвечает за: перевести пиццу из формата бэкенда в формат приложения.
// Это ЕДИНСТВЕННОЕ место в проекте, которое знает про pizza_name и копейки.
import type { Pizza } from '../types';
import type { ApiPizza } from './fake-backend';

export const toPizza = (raw: ApiPizza): Pizza => ({
  id: raw.pizza_id,
  name: raw.pizza_name,
  price: raw.price_kopecks / 100,
  isVegan: raw.is_vegan === 1,
  createdAt: new Date(raw.created_at),
});
