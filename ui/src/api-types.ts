export interface CountrySerializer {
    name: string;
    code: string;
    unicode_flag: string;
}

export interface ServiceSerializer {
    name: string;
}

export interface RouteSerializer {
    name: string;
    host_country: CountrySerializer;
}

export interface ProcessStepSerializer {
    sequence_number: number;
    service: ServiceSerializer;
}

export interface ProcessSerializer {
    id?: number;
    route: RouteSerializer;
    nationality: CountrySerializer;
    home_country: CountrySerializer;
    steps: ProcessStepSerializer[];
}

export interface UserSerializer {
    first_name?: string;
    last_name?: string;
    email?: string;
}

export interface ClientSerializer {
    name: string;
}

export interface EmployeeSerializer {
    user: UserSerializer;
    employer: ClientSerializer;
    home_country: CountrySerializer;
    nationalities: CountrySerializer[];
}

export interface ClientContactSerializer {
    user: UserSerializer;
    client: ClientSerializer;
}

export interface ProviderSerializer {
    name: string;
}

export interface ProviderContactSerializer {
    user: UserSerializer;
    provider: ProviderSerializer;
}

export interface CaseSerializer {
    id?: number;
    employee: EmployeeSerializer;
    process: ProcessSerializer;
    target_entry_date: string;
    target_exit_date: string;
    provider_contact: ProviderContactSerializer;
}

