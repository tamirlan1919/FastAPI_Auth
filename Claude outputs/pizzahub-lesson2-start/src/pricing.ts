// Правила цен. Отвечает за ОДНО: посчитать, сколько стоит позиция и заказ.
import type { CartItem, Size } from './types';

const SIZE_MULTIPLIER: Record<Size, number> = { S: 0.8, M: 1, L: 1.3 };
const PROMO_CODES: Record<string, number> = { PIZZA10: 0.1, HAPPY20: 0.2 };

export const itemPrice = (item: CartItem): number =>
  Math.round(item.pizza.price * SIZE_MULTIPLIER[item.size]) * item.qty;

export const calcTotal = (items: CartItem[], promoCode: string | null = null): number => {
  const subtotal = items.reduce((sum, item) => sum + itemPrice(item), 0);
  const discount = promoCode ? (PROMO_CODES[promoCode] ?? 0) : 0;
  return Math.round(subtotal * (1 - discount));
};
