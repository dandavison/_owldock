import {
  CaseSerializer,
  ClientSerializer,
  CountrySerializer,
  EmployeeSerializer,
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

export function NullEmployee(): EmployeeSerializer {
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
    employee: NullEmployee(),
    process: NullProcess(),
    target_entry_date: "",
    target_exit_date: "",
    provider_contact: NullProviderContact()
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

export function employeeIsNull(employee: EmployeeSerializer): boolean {
  return userIsNull(employee.user);
}
