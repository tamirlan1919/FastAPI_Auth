// «Компонент» шапки сайта. Отвечает за: показать бейдж корзины.
import { cartStore } from '../store/cart.store';

export function renderHeader(): void {
  console.log(`🛒 Шапка: в корзине ${cartStore.count()} шт.`);
}
