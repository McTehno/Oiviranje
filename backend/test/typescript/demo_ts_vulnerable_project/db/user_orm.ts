export async function findUserByName(req: any, prisma: any) {
    const name: string = req.body.name;
    return await prisma.$queryRaw`SELECT * FROM users WHERE name = ${name}`;

}