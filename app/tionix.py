# -*- coding: utf-8 -*-
import csv
import cmd
import datetime
import smtplib
from email.mime.text import MIMEText
CSV_FORMAT = "csv"


class EmailSender(object):
    """
       class which can send messages to employees by email
    """

    def __init__(self, user, pwd):
        """

        :param user: username for gmail
        :param pwd: password
        """
        self.user = user
        self.pwd = pwd
        self.server = None

    def connect(self):
        """
        connecting to gmail smpt server
        :return:
        """
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.user, self.pwd)

    def send_message(self, to):
        """
        send messages to list of employees
        :param to: list of emails or email in str
        :return: response from server
        """
        to_list = []
        if isinstance(to, basestring):
            to_list.append(to)
        else:
            to_list.extend(to)
        msg = MIMEText(" Hello ")
        msg['Subject'] = 'The contents of tionix test task'
        msg['From'] = self.user
        return self.server.sendmail(
            from_addr='.'.join([self.user, 'gmail', 'com']),
            to_addrs=to_list, msg=msg.as_string())

    def disconnect(self):
        """
        close connection
        :return: server response
        """
        return self.server.quit()


class Employee(object):

    def __init__(self, employee_id, name, contact_info,
                 date_begin, date_end, hours):
        """
        date being < date end
        конец - Начало < 24
        0 < hours < 12
        :param employee_id: emp id in int type
        :param name: emp name in str type
        :param contact_info: contact info(e-mail) in str
        :param date_begin: begin date in datetime
        :param date_end: end date in datetime
        :param hours: hours count in int
        """
        self.employee_id = int(employee_id)
        self.name = name
        self.contact_info = contact_info
        self.hours = int(hours)
        self.days = 1
        self.date_begin = datetime.datetime.strptime(
            date_begin, "%Y-%m-%d %H:%M:%S")
        self.date_end = datetime.datetime.strptime(
            date_end, "%Y-%m-%d %H:%M:%S")


    def __str__(self):
        return " ".join(['id:', str(self.employee_id), 'name:', self.name,
                         'contact_info:', self.contact_info,
                         'hours:', str(self.hours)])

    def is_valid(self):
        """
        date being < date end
        0 < hours < 12
        date end - date begin < 24

        :return: bool
        """
        return (self.date_begin < self.date_end and 0 < self.hours < 12 and
                (self.date_end - self.date_begin).days < 1)


class EmployeeFactory(object):
    """
        Factory for creating and working with Employee class
    """

    def __init__(self):
        self.employees = dict()

    def add_employee(self, employee):
        """
        add or update employee to employees factory
        :param employee: employee class exemplar
        :return:
        """
        if employee.employee_id in self.employees:
            self.employees[employee.employee_id].hours += employee.hours
            self.employees[employee.employee_id].days += 1
        else:
            self.employees[employee.employee_id] = employee

    def get_expired(self, expired_time=15):
        """
        Get employees which have hours gte expired_time
        :param expired_time:
        :return: list of employees
        """
        return filter(lambda emp: emp.hours >= expired_time,
                      self.employees.values())

    @staticmethod
    def get_load_file_format(args):
        """
        Check that we have valid filename in args and return file name
        :param args: args from cli
        :return:
        """
        if args:
            args_list = args.split(" ")
            file_name = args_list[0]
            splitted_file = file_name.split(".")
            if len(splitted_file) == 2 and splitted_file[1] == CSV_FORMAT:
                return file_name
        return ''

    def load_employees_from_file(self, filename):
        """

        :param filename: path to file
        :return:
        """
        with open(filename) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                new_emp = Employee(*row)
                if new_emp.is_valid():
                    self.add_employee(new_emp)
                else:
                    print "Unable to create employee {emp}".format(emp=new_emp)

    def show_all(self):
        """
            Shows to cli all employees which present in employees factory
        :return:
        """
        for emp in self.employees.values():
            print emp

    def send_messages(self, expired_time=15):
        """
        send messages to employees which have hourse gte expired_time
        :param expired_time: expired time in int format
        :return:
        """

        expired_emp = self.get_expired(expired_time)
        if expired_emp:
            sender = EmailSender("tionix.test", "tionix.test123")
            sender.connect()
            emails_list = [emp.contact_info for emp in expired_emp]
            sender.send_message(emails_list)
            sender.disconnect()
            print "emails was send to \n".join(emails_list)


class Cli(cmd.Cmd):
    """
        command line interface for app
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.intro = ("Welcome\n Enter 'help' for more information\n "
                      "to exit type ctrl + C")
        self.doc_header = (
            "Available commands (for help abput  specific command"
            "enter 'help _command_')")
        self.employees = EmployeeFactory()

    def default(self, line):
        print "Command does not exist"

    def do_load(self, args):
        """
            read
            load csv file to memory
        """
        filename = self.employees.get_load_file_format(args)
        if not filename:
            print "file does not valid"
            return
        try:
            self.employees.load_employees_from_file(filename)
        except IOError as e:
            print e
            return
        self.employees.send_messages()
        self.employees.show_all()

if __name__ == "__main__":
    cli = Cli()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print "ending session..."
