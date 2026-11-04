// SINGLETON. Корзина покупателя — одна на всё приложение.
// Отвечает за: хранить позиции корзины и отвечать «сколько штук» и «на какую сумму».
import { calcTotal } from '../pricing';
import type { CartItem, Pizza, Size } from '../types';

class CartStore {
  private items: CartItem[] = [];

  add(pizza: Pizza, size: Size = 'M', qty = 1): void {
    const same = this.items.find((i) => i.pizza.id === pizza.id && i.size === size);
    if (same) same.qty += qty;
    else this.items.push({ pizza, size, qty });
  }

  getItems(): CartItem[] {
    return structuredClone(this.items);   // отдаём копию, а не свой массив (почему — в шаге Prototype)
  }

  count(): number {
    return this.items.reduce((sum, i) => sum + i.qty, 0);
  }

  total(): number {
    return calcTotal(this.items);
  }

  clear(): void {
    this.items = [];
  }
}

// Экспортируем ЭКЗЕМПЛЯР, а не класс: модуль выполнится один раз,
// и все, кто сделает import { cartStore }, получат один и тот же объект.
export const cartStore = new CartStore();
