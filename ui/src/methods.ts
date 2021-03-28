import { EmployeeSerializer } from "./api-types";

export function employeeUnicodeFlags(employee: EmployeeSerializer): string {
  return employee.nationalities
    .map(nationality => nationality.unicode_flag)
    .join(" ");
}
