export interface CreateStudyProps {
    onClose: () => void
  }
  
  export interface Question {
    id: number
    text: string
    important: boolean
    topic: string
  }
  
  export interface ScreenerQuestion {
    id: number
    text: string
  }
  
  export interface User {
    id: number
    name: string
    age: number
    gender: string
    income: string
  }
  
  export interface TableProps extends React.HTMLAttributes<HTMLTableElement> {
    children?: React.ReactNode
  }
  
  export interface TableHeaderProps extends React.HTMLAttributes<HTMLTableSectionElement> {
    children?: React.ReactNode
  }
  
  export interface TableBodyProps extends React.HTMLAttributes<HTMLTableSectionElement> {
    children?: React.ReactNode
  }
  
  export interface TableRowProps extends React.HTMLAttributes<HTMLTableRowElement> {
    children?: React.ReactNode
  }
  
  export interface TableHeadProps extends React.ThHTMLAttributes<HTMLTableCellElement> {
    children?: React.ReactNode
  }
  
  export interface TableCellProps extends React.TdHTMLAttributes<HTMLTableCellElement> {
    children?: React.ReactNode
  }