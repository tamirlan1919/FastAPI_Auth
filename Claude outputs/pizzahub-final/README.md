# PizzaHub — готовый проект урока «Паттерны: порождающие и структурные»

Нужен Node.js 20+.

    npm install
    npm run dev        # сценарий: меню → корзина → форма → оформление → повтор заказа
    npm run typecheck  # проверка типов

| Паттерн   | Файл                                |
|-----------|-------------------------------------|
| Singleton | src/store/cart.store.ts             |
| Factory   | src/notifications/toast.factory.ts  |
| Builder   | src/orders/order.builder.ts         |
| Prototype | src/orders/repeat-order.ts          |
| Adapter   | src/api/pizza.adapter.ts            |
| Decorator | src/lib/decorators.ts               |
| Proxy     | src/forms/order-form.proxy.ts       |
| Facade    | src/checkout/checkout.facade.ts     |

«Сервер» (src/api/fake-backend.ts) специально падает в 30% запросов — повторы делает withRetry.
