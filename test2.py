class Employee:

    raise_amt = 1.02
    total_employee = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

        Employee.total_employee += 1

    def fullname(self):
        return "{} {}".format(self.first, self.last)

    def email(self):
        return "{}.{}@email.com".format(self.first, self.last)

    def raise_pay(self):
        return self.pay * self.raise_amt


employee_1 = Employee("John", "Doe", 50000)
employee_2 = Employee("Jane", "Doe", 40000)
print(employee_1.fullname())
print(employee_1.email())
print(employee_1.raise_pay())
print(employee_2.raise_pay())

print(Employee.total_employee)
