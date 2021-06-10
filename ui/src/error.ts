enum OwldockErrorName {
  CircularDependency = "Circular Dependency",
}

class OwldockError {
  name: OwldockErrorName;
  message: string;

  constructor(name: OwldockErrorName, message: string) {
    this.name = name;
    this.message = message;
  }
}

export class CircularDependencyError extends OwldockError {
  constructor(message: string) {
    super(OwldockErrorName.CircularDependency, message);
  }
}
