export interface CountrySerializer {
    name: string;
    code: string;
    unicode_flag: string;
}

export interface ServiceSerializer {
    name: string;
}

export interface ProcessSerializer {
    name: string;
    host_country: CountrySerializer;
}

export interface ProcessFlowStepSerializer {
    sequence_number: number;
    service: ServiceSerializer;
}

export interface ProcessFlowSerializer {
    nationality: CountrySerializer;
    home_country: CountrySerializer;
    steps: ProcessFlowStepSerializer[];
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
    client_contact: ClientContactSerializer;
    employee: EmployeeSerializer;
    process: ProcessSerializer;
    host_country: CountrySerializer;
    target_entry_date: string;
    provider_contact: ProviderContactSerializer;
}

