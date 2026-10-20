// FACADE. Отвечает за: одну кнопку «Оформить заказ».
// Внутри координирует корзину, строитель заказа, оплату и уведомления.
// Снаружи — одна функция с понятным результатом.
import { notify } from '../notifications/toast.factory';
import { OrderBuilder } from '../orders/order.builder';
import { cartStore } from '../store/cart.store';
import type { Order } from '../types';
import { payWithCard } from './payment';

export interface CheckoutInput {
  address: string;
  phone: string;
  promoCode?: string;
}

export type CheckoutResult =
  | { ok: true; order: Order; paymentId: string }
  | { ok: false; error: string };

export async function checkout(input: CheckoutInput): Promise<CheckoutResult> {
  try {
    const order = new OrderBuilder()                 // Builder
      .fromCart(cartStore.getItems())                // Singleton
      .to(input.address)
      .withPhone(input.phone)
      .withPromo(input.promoCode ?? null)
      .build();

    const paymentId = await payWithCard(order.total);
    cartStore.clear();
    notify('success', `Заказ №${order.id} оплачен: ${order.total} ₽`);   // Factory
    return { ok: true, order, paymentId };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    notify('error', `Заказ не оформлен: ${message}`);
    return { ok: false, error: message };
  }
}
