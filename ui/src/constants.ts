/// TODO: these are defined server-side, and duplicated here. The definitions
/// here would ideally be autogenerated, in a similar way to the interface
/// definitions in pydantic-autogenerated-interfaces.ts.

export enum Role {
  // Hack: these string values are used to construct URLs
  Admin = "admin",
  ClientContact = "client-contact",
  ProviderContact = "provider-contact",
  Invalid = "INVALID",
}

export enum HomeOrHostCountry {
  HomeCountry = "HOME_COUNTRY",
  HostCountry = "HOST_COUNTRY",
  None = "",
}

export const HomeOrHostCountryDisplayName: Map<
  HomeOrHostCountry,
  string
> = new Map([
  [HomeOrHostCountry.HomeCountry, "Home Country"],
  [HomeOrHostCountry.HostCountry, "Host Country"],
  [HomeOrHostCountry.None, ""],
]);
