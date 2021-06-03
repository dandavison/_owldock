import Cookies from "js-cookie";

export enum Role {
  // Hack: these string values are used to construct URLs
  Admin = "admin",
  ClientContact = "client-contact",
  ProviderContact = "provider-contact",
  Invalid = "INVALID",
}

export function getRole(): Role {
  switch (Cookies.get("role")) {
    case "admin":
      return Role.Admin;
    case "client-contact":
      return Role.ClientContact;
    case "provider-contact":
      return Role.ProviderContact;
    default:
      return Role.Invalid;
  }
}

export function isAdmin(): boolean {
  return getRole() == Role.Admin;
}

export function isClientContact(): boolean {
  return getRole() == Role.ClientContact;
}

export function isProviderContact(): boolean {
  return getRole() == Role.ProviderContact;
}
