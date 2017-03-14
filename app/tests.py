import unittest
from tionix import EmailSender, Employee, EmployeeFactory, Cli


class TestEmailSender(unittest.TestCase):

    def test_connect(self):
        sender = EmailSender("sender.user", "password")
        sender.connect()
        # server response code (e.g. '250', or such, if all goes well)
        self.assertEquals(sender.server.noop()[0], 250,
                          "bad response from server")

    def test_send_message(self):
        sender = EmailSender("sender.user", "password"
        sender.connect()
        # server response code (e.g. '250', or such, if all goes well)
        self.assertEquals(sender.server.noop()[0], 250,
                          "bad response from server")
        # If all addresses are accepted, then the method will return an
        # empty dictionary.
        resp = sender.send_message(to="dubrovin.ruslan@gmail.com")
        self.assertEquals(resp, {}, "bad response from server")

    def test_disconnect(self):
        sender = EmailSender("sender.user", "password"
        sender.connect()
        # server response code (e.g. '250', or such, if all goes well)
        self.assertEquals(sender.server.noop()[0], 250,
                          "bad response from server")
        resp = sender.disconnect()
        # server response code (e.g. '221', or such, if all goes well)
        self.assertEquals(resp[0], 221, "bad response from server")


class TestEmployee(unittest.TestCase):
    test_emp_data = {
        "employee_id": "1",
        "name": "testname",
        "contact_info": "test@mail.com",
        "date_begin": "2016-01-01 15:32:11",
        "date_end": "2016-01-01 21:32:11",
        "hours": "6"
    }

    def test_emp_create(self):
        emp = Employee(**self.test_emp_data)
        self.assertEquals(
            emp.employee_id, int(self.test_emp_data['employee_id']),
            "Incorrect id")
        self.assertEquals(
            emp.name, self.test_emp_data['name'], "Incorrect name")
        self.assertEquals(
            emp.contact_info, self.test_emp_data['contact_info'],
            "Incorrect contact info")
        self.assertEquals(emp.hours, int(self.test_emp_data['hours']),
                          "Incorrect hours")
        self.assertTrue(emp.is_valid(), "Invalid dates")


class TestEmployeeFactory(TestEmployee):

    def test_factory_init(self):
        emp_factory = EmployeeFactory()

        self.assertFalse(emp_factory.employees,
                         "Employees factory should be empty")

    def test_factory_add_emp(self):
        emp_factory = EmployeeFactory()

        self.assertFalse(emp_factory.employees,
                         "Employees factory should be empty")
        emp_factory.add_employee(Employee(**self.test_emp_data))

        self.assertEquals(len(emp_factory.employees), 1,
                          "Employee factory empty")


class TestCli(unittest.TestCase):
    def test_cli(self):
        cli = Cli()
        cli.do_load("test_data/test.csv")
        self.assertEquals(len(cli.employees.employees), 1,
                          "Employee factory empty")


if __name__ == '__main__':
    unittest.main()
