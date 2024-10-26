import { z } from "zod"
import { useForm } from "react-hook-form"

const formSchema = z.object({
  username: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }),
})

function onSubmit(values) {
  console.log(values)
}

import {
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

import { Button } from "./ui/button"

export function NewOrderForm () {

  const {register, handleSubmit} = useForm();


  return (
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        <Label>Id</Label>
        <Input placehoder="id do pedido" {...register('id')}/>
        <Label>Produto</Label>
        <Input placehoder="produto" {...register('product')}/>
        <Button type="submit">Submit</Button>
      </form>
  )
}
