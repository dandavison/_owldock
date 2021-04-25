import Cookies from "js-cookie";

export enum Role {
  // Hack: these string values are used to construct URLs
  ClientContact = "client-contact",
  ProviderContact = "provider-contact",
  Invalid = "INVALID",
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
