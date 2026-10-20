// DECORATOR. Отвечает за: добавлять функциям поведение (лог, повтор, кеш), не меняя их код.
// Каждая обёртка принимает функцию и возвращает функцию С ТЕМ ЖЕ интерфейсом.

type AsyncFn<A extends unknown[], R> = (...args: A) => Promise<R>;

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const withLogging = <A extends unknown[], R>(fn: AsyncFn<A, R>, name: string): AsyncFn<A, R> =>
  async (...args) => {
    const start = performance.now();
    try {
      return await fn(...args);
    } finally {
      console.log(`⏱  ${name}: ${Math.round(performance.now() - start)} мс`);
    }
  };

export const withRetry = <A extends unknown[], R>(fn: AsyncFn<A, R>, attempts = 3): AsyncFn<A, R> =>
  async (...args) => {
    let lastError: unknown;
    for (let attempt = 1; attempt <= attempts; attempt++) {
      try {
        return await fn(...args);
      } catch (error) {
        lastError = error;
        console.log(`↻  попытка ${attempt} не удалась: ${(error as Error).message}`);
        if (attempt < attempts) await sleep(200 * attempt);
      }
    }
    throw lastError;
  };

export const withCache = <A extends unknown[], R>(fn: AsyncFn<A, R>, ttlMs: number): AsyncFn<A, R> => {
  const cache = new Map<string, { value: R; expiresAt: number }>();
  return async (...args) => {
    const key = JSON.stringify(args);
    const hit = cache.get(key);
    if (hit && hit.expiresAt > Date.now()) return hit.value;
    const value = await fn(...args);
    cache.set(key, { value, expiresAt: Date.now() + ttlMs });
    return value;
  };
};
