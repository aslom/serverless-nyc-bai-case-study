function main(params) {
  console.log(params)
  if (params) {
    return { greeting: `The message ${params.messages[0].value} arrived on the kafka topic ${params.messages[0].topic}` };
  }
  return { greeting: 'Hello stranger!' };
}
