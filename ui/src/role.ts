import Cookies from "js-cookie";

export enum Role {
  ClientContact,
  ProviderContact,
  Invalid
}

export function getRole(): Role {
  switch (Cookies.get("role")) {
    case "client-contact":
      return Role.ClientContact;
    case "provider-contact":
      return Role.ProviderContact;
    default:
      return Role.Invalid;
  }
}

export function isClientContact(): boolean {
  return getRole() == Role.ClientContact;
}

export function isProviderContact(): boolean {
  return getRole() == Role.ProviderContact;
}
