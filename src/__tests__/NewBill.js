/**
 * @jest-environment jsdom
 */

import { screen, fireEvent, waitFor } from "@testing-library/dom"
import NewBillUI from "../views/NewBillUI.js"
import NewBill from "../containers/NewBill.js"
import { ROUTES, ROUTES_PATH } from "../constants/routes.js"
import { localStorageMock } from "../__mocks__/localStorage.js"
import mockStore from "../__mocks__/store"
import router from "../app/Router.js"

jest.mock("../app/store", () => mockStore)

describe("Given I am connected as an employee", () => {
  describe("When I am on NewBill Page", () => {
    beforeEach(() => {
      document.body.innerHTML = ''
      Object.defineProperty(window, 'localStorage', { value: localStorageMock })
      window.localStorage.setItem('user', JSON.stringify({
        type: 'Employee',
        email: 'employee@test.tld'
      }))
    })

    test("Then the form should be displayed", () => {
      const html = NewBillUI()
      document.body.innerHTML = html
      expect(screen.getByTestId('form-new-bill')).toBeTruthy()
    })

    test("Then mail icon in vertical layout should be highlighted", async () => {
      const root = document.createElement("div")
      root.setAttribute("id", "root")
      document.body.append(root)
      router()
      window.onNavigate(ROUTES_PATH.NewBill)
      await waitFor(() => screen.getByTestId('icon-mail'))
      const mailIcon = screen.getByTestId('icon-mail')
      expect(mailIcon.classList.contains('active-icon')).toBe(true)
    })
  })

  describe("When I upload a file with valid extension", () => {
    test("Then the file should be accepted", () => {
      document.body.innerHTML = ''
      Object.defineProperty(window, 'localStorage', { value: localStorageMock })
      window.localStorage.setItem('user', JSON.stringify({
        type: 'Employee',
        email: 'employee@test.tld'
      }))

      document.body.innerHTML = NewBillUI()

      const onNavigate = jest.fn()
      const newBill = new NewBill({
        document,
        onNavigate,
        store: mockStore,
        localStorage: window.localStorage
      })

      const handleChangeFile = jest.fn(newBill.handleChangeFile)
      const fileInput = screen.getByTestId('file')
      fileInput.addEventListener('change', handleChangeFile)

      const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
      Object.defineProperty(fileInput, 'files', { value: [file] })

      fireEvent.change(fileInput)
      expect(handleChangeFile).toHaveBeenCalled()
      expect(fileInput.files[0].name).toBe('test.jpg')
    })
  })

  describe("When I upload a file with invalid extension", () => {
    test("Then the file should be rejected and input cleared", () => {
      document.body.innerHTML = ''
      Object.defineProperty(window, 'localStorage', { value: localStorageMock })
      window.localStorage.setItem('user', JSON.stringify({
        type: 'Employee',
        email: 'employee@test.tld'
      }))

      document.body.innerHTML = NewBillUI()

      const onNavigate = jest.fn()
      const newBill = new NewBill({
        document,
        onNavigate,
        store: mockStore,
        localStorage: window.localStorage
      })

      const fileInput = screen.getByTestId('file')
      const file = new File(['test'], 'test.pdf', { type: 'application/pdf' })
      Object.defineProperty(fileInput, 'files', { value: [file] })
      Object.defineProperty(fileInput, 'value', { value: 'C:\\fakepath\\test.pdf', writable: true })

      fireEvent.change(fileInput)

      expect(newBill.fileName).toBeNull()
      expect(newBill.fileUrl).toBeNull()
    })
  })

  describe("When I submit the form with valid data", () => {
    test("Then the bill should be created and I should navigate to Bills page", () => {
      document.body.innerHTML = ''
      Object.defineProperty(window, 'localStorage', { value: localStorageMock })
      window.localStorage.setItem('user', JSON.stringify({
        type: 'Employee',
        email: 'employee@test.tld'
      }))

      document.body.innerHTML = NewBillUI()

      const onNavigate = jest.fn()
      const newBill = new NewBill({
        document,
        onNavigate,
        store: mockStore,
        localStorage: window.localStorage
      })

      const form = screen.getByTestId('form-new-bill')
      const handleSubmit = jest.fn(newBill.handleSubmit)
      form.addEventListener('submit', handleSubmit)

      screen.getByTestId('expense-type').value = 'Transports'
      screen.getByTestId('expense-name').value = 'Test expense'
      screen.getByTestId('datepicker').value = '2023-01-01'
      screen.getByTestId('amount').value = '100'
      screen.getByTestId('vat').value = '20'
      screen.getByTestId('pct').value = '20'
      screen.getByTestId('commentary').value = 'Test comment'
      newBill.fileUrl = 'https://test.com/test.jpg'
      newBill.fileName = 'test.jpg'

      fireEvent.submit(form)

      expect(handleSubmit).toHaveBeenCalled()
      expect(onNavigate).toHaveBeenCalledWith(ROUTES_PATH['Bills'])
    })
  })
})

// Test d'integration POST
describe("Given I am a user connected as Employee", () => {
  describe("When I create a new bill", () => {
    beforeEach(() => {
      document.body.innerHTML = ''
      jest.spyOn(mockStore, "bills")
      Object.defineProperty(window, 'localStorage', { value: localStorageMock })
      window.localStorage.setItem('user', JSON.stringify({
        type: 'Employee',
        email: 'employee@test.tld'
      }))
    })

    test("Then it should create bill via mock API POST", async () => {
      const html = NewBillUI()
      document.body.innerHTML = html

      const onNavigate = jest.fn()
      const newBill = new NewBill({
        document,
        onNavigate,
        store: mockStore,
        localStorage: window.localStorage
      })

      const fileInput = screen.getByTestId('file')
      const file = new File(['test'], 'test.png', { type: 'image/png' })
      Object.defineProperty(fileInput, 'files', { value: [file] })
      Object.defineProperty(fileInput, 'value', { value: 'C:\\fakepath\\test.png', writable: true })

      fireEvent.change(fileInput)

      await new Promise(process.nextTick)

      expect(newBill.billId).toBe('1234')
      expect(newBill.fileUrl).toBe('https://localhost:3456/images/test.jpg')
    })

    describe("When an error occurs on API", () => {
      test("Then it should fail with 404 error", async () => {
        mockStore.bills.mockImplementationOnce(() => {
          return {
            create: () => {
              return Promise.reject(new Error("Erreur 404"))
            }
          }
        })

        const html = NewBillUI()
        document.body.innerHTML = html

        const onNavigate = jest.fn()
        const newBill = new NewBill({
          document,
          onNavigate,
          store: mockStore,
          localStorage: window.localStorage
        })

        const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {})

        const fileInput = screen.getByTestId('file')
        const file = new File(['test'], 'test.png', { type: 'image/png' })
        Object.defineProperty(fileInput, 'files', { value: [file] })
        Object.defineProperty(fileInput, 'value', { value: 'C:\\fakepath\\test.png', writable: true })

        fireEvent.change(fileInput)
        await new Promise(process.nextTick)

        expect(consoleError).toHaveBeenCalled()
        consoleError.mockRestore()
      })

      test("Then it should fail with 500 error", async () => {
        mockStore.bills.mockImplementationOnce(() => {
          return {
            create: () => {
              return Promise.reject(new Error("Erreur 500"))
            }
          }
        })

        const html = NewBillUI()
        document.body.innerHTML = html

        const onNavigate = jest.fn()
        const newBill = new NewBill({
          document,
          onNavigate,
          store: mockStore,
          localStorage: window.localStorage
        })

        const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {})

        const fileInput = screen.getByTestId('file')
        const file = new File(['test'], 'test.png', { type: 'image/png' })
        Object.defineProperty(fileInput, 'files', { value: [file] })
        Object.defineProperty(fileInput, 'value', { value: 'C:\\fakepath\\test.png', writable: true })

        fireEvent.change(fileInput)
        await new Promise(process.nextTick)

        expect(consoleError).toHaveBeenCalled()
        consoleError.mockRestore()
      })
    })
  })
})
