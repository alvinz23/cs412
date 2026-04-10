export type AuthData = {
  token: string;
  profileId: number | null;
  username: string;
};

// Super simple in-memory auth store for this app.
let authData: AuthData = {
  token: '',
  profileId: null,
  username: '',
};

export function getAuthData(): AuthData {
  // Read token/profile info anywhere in tabs.
  return authData;
}

export function setAuthData(next: AuthData): void {
  // Save token/profile info after login.
  authData = next;
}

export function clearAuthData(): void {
  // Clear token on logout/401.
  authData = { token: '', profileId: null, username: '' };
}
