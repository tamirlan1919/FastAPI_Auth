// Имитация сервера. Отвечает за: отдать «сырые» данные так, как их отдал бы настоящий бэкенд —
// в своём формате (snake_case, копейки), с задержкой сети и иногда с ошибкой.
import { readFile } from 'node:fs/promises';

export interface ApiPizza {
  pizza_id: number;
  pizza_name: string;
  price_kopecks: number;
  is_vegan: 0 | 1;
  created_at: string;
}

const FAIL_RATE = 0.3;            // 30% запросов падают — как мобильный интернет в метро
let requestCount = 0;

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export async function getPizzasFromServer(): Promise<ApiPizza[]> {
  requestCount++;
  await sleep(300);
  if (Math.random() < FAIL_RATE) {
    throw new Error('503 Service Unavailable');
  }
  const file = new URL('../../data/pizzas.json', import.meta.url);
  return JSON.parse(await readFile(file, 'utf-8'));
}

export const getRequestCount = () => requestCount;
