// FACTORY METHOD. Отвечает за: решить, КАКОЕ уведомление создать, в одном месте.
// Остальной код говорит «покажи ошибку» и не знает про классы ErrorToast и т.п.

export interface Toast {
  show(): void;
}

class SuccessToast implements Toast {
  constructor(private message: string) {}
  show() { console.log(`✅ ${this.message}`); }
}

class ErrorToast implements Toast {
  constructor(private message: string) {}
  show() { console.error(`❌ ${this.message}`); }   // ошибки — в stderr
}

class InfoToast implements Toast {
  constructor(private message: string) {}
  show() { console.log(`ℹ️  ${this.message}`); }
}

export type ToastType = 'success' | 'error' | 'info';

// Реестр «тип → как создать». Новый тип = одна строка здесь.
// Record<ToastType, ...> заставит TypeScript проверить, что ни один тип не забыт.
const registry: Record<ToastType, (message: string) => Toast> = {
  success: (m) => new SuccessToast(m),
  error: (m) => new ErrorToast(m),
  info: (m) => new InfoToast(m),
};

export const createToast = (type: ToastType, message: string): Toast => registry[type](message);

// Удобный шорткат: создать и сразу показать
export const notify = (type: ToastType, message: string): void => createToast(type, message).show();
