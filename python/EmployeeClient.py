from __future__ import print_function
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const


def run():
    with grpc.insecure_channel(const.IP + ':' + const.PORT) as channel:
        stub = EmployeeService_pb2_grpc.EmployeeServiceStub(channel)

        # Query an employee's data
        response = stub.GetEmployeeDataFromID(EmployeeService_pb2.EmployeeID(id=101))
        print('Employee\'s data: ' + str(response))

        # Add a new employee
        response = stub.CreateEmployee(
            EmployeeService_pb2.EmployeeData(id=301, name='Jose da Silva', title='Programmer'))
        print('Added new employee ' + response.status)

        # Change an employee's title
        response = stub.UpdateEmployeeTitle(EmployeeService_pb2.EmployeeTitleUpdate(id=301, title='Senior Programmer'))
        print('Updated employee ' + response.status)

        # Delete an employee
        response = stub.DeleteEmployee(EmployeeService_pb2.EmployeeID(id=201))
        print('Deleted employee ' + response.status)

        # List all employees
        response = stub.ListAllEmployees(EmployeeService_pb2.EmptyMessage())
        print('All employees:')
        for emp in response.employee_data:
            print(f"ID: {emp.id}, Name: {emp.name}, Title: {emp.title}")

        # Search for an employee by name
        name_to_search = 'Jose da Silva'
        found = False
        for emp in response.employee_data:
            if emp.name == name_to_search:
                found = True
                print(f"{name_to_search} found. ID: {emp.id}, Title: {emp.title}")
        if not found:
            print(f"{name_to_search} not found.")

        # Remove an employee by ID
        id_to_remove = 101
        found = False
        for emp in response.employee_data:
            if emp.id == id_to_remove:
                found = True
                response = stub.DeleteEmployee(EmployeeService_pb2.EmployeeID(id=id_to_remove))
                print(f"Employee with ID {id_to_remove} removed. Status: {response.status}")
                break
        if not found:
            print(f"Employee with ID {id_to_remove} not found.")

        # Add a new employee at a specific position in the list
        new_employee = {'id': 401, 'name': 'Maria Oliveira', 'title': 'Database Administrator'}
        index_to_insert = 1
        emp_data_list = response.employee_data
        emp_data_list.insert(index_to_insert, EmployeeService_pb2.EmployeeData(
            id=new_employee['id'], name=new_employee['name'], title=new_employee['title']))
        response = stub.ListAllEmployees(EmployeeService_pb2.EmptyMessage())
        print('All employees after insertion:')
        for emp in response.employee_data:
            print(f"ID: {emp.id}, Name: {emp.name}, Title: {emp.title}")

        # Sort the list of employees by name
        emp_data_list = sorted(emp_data_list, key=lambda emp: emp.name)
        response = EmployeeService_pb2.EmployeeDataList()
        response.employee_data.extend(emp_data_list)
        print('All employees sorted by name:')
        for emp in response.employee_data:
            print(f"ID: {emp.id}, Name: {emp.name}, Title: {emp.title}")


if __name__ == '__main__':
    logging.basicConfig()
    run()
