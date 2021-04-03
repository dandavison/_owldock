import {
  CaseSerializer,
  ClientSerializer,
  CountrySerializer,
  ApplicantSerializer,
  ProcessSerializer,
  ProviderContactSerializer,
  ProviderSerializer,
  RouteSerializer,
  UserSerializer
} from "./api-types";

function NullCountry(): CountrySerializer {
  return {
    name: "",
    code: "",
    unicode_flag: ""
  };
}

function NullRoute(): RouteSerializer {
  return {
    name: "",
    host_country: NullCountry()
  };
}

function NullProcess(): ProcessSerializer {
  return {
    id: undefined,
    route: NullRoute(),
    nationality: NullCountry(),
    home_country: NullCountry(),
    steps: []
  };
}

function NullUser(): UserSerializer {
  return {};
}

function NullClient(): ClientSerializer {
  return { name: "" };
}

export function NullApplicant(): ApplicantSerializer {
  return {
    user: NullUser(),
    employer: NullClient(),
    home_country: NullCountry(),
    nationalities: []
  };
}

export function NullProvider(): ProviderSerializer {
  return {
    name: ""
  };
}

export function NullProviderContact(): ProviderContactSerializer {
  return {
    user: NullUser(),
    provider: NullProvider()
  };
}

export function NullCase(): CaseSerializer {
  return {
    id: undefined,
    applicant: NullApplicant(),
    process: NullProcess(),
    provider_contact: NullProviderContact(),
    target_entry_date: "",
    target_exit_date: ""
  };
}

// TODO: better options here?

export function countryIsNull(country: CountrySerializer): boolean {
  return !country.code;
}

export function processIsNull(process: ProcessSerializer): boolean {
  return routeIsNull(process.route);
}

export function routeIsNull(route: RouteSerializer): boolean {
  return !route.name || countryIsNull(route.host_country);
}
export function userIsNull(user: UserSerializer): boolean {
  return !user.first_name;
}

export function applicantIsNull(applicant: ApplicantSerializer): boolean {
  return userIsNull(applicant.user);
}

export function providerContactIsNull(
  providerContact: ProviderContactSerializer
): boolean {
  return userIsNull(providerContact.user);
}
