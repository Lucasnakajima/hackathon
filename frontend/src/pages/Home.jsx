import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

import { Button } from "@/components/ui/button";

import { NewOrderForm } from '../components/NewOrderForm';



export default function Home() {
  return (
    <div className="col-span-10 p-10">
    <h1 className=" my-10 text-3xl">Encomendas</h1>
    <Table>
      <TableCaption>Uma lista das suas recentes encomendas.</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[100px]">Id</TableHead>
          <TableHead>Method</TableHead>
          <TableHead className="text-right">Amount</TableHead>
          <TableHead>Status</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          <TableCell className="font-medium">INV001</TableCell>
          <TableCell>Credit Card</TableCell>
          <TableCell className="text-right">$250.00</TableCell>
          <TableCell>Paid</TableCell>
        </TableRow>
      </TableBody>
    </Table>
    <Dialog>
      <DialogTrigger>
        <Button variant="outline">Adicionar encomenda</Button>
        </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nova Encomenda</DialogTitle>
          <NewOrderForm/>
        </DialogHeader>
      </DialogContent>
    </Dialog>

    </div>
  );
};