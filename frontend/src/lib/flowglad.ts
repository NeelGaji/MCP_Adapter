import { FlowgladServer } from '@flowglad/nextjs/server'

/**
 * FlowGlad server factory function.
 * 
 * @param customerExternalId - Your app's user/organization ID (NOT Flowglad's customer ID)
 * @returns FlowgladServer instance configured for this customer
 */
export const flowglad = (customerExternalId: string) => {
    return new FlowgladServer({
        customerExternalId,
        getCustomerDetails: async (customerExternalId) => {
            // TODO: Replace with actual user lookup from your auth/database
            // For example, if using Next-Auth:
            //   const user = await prisma.user.findUnique({ where: { id: customerExternalId } })
            //   return { email: user.email, name: user.name }

            return {
                email: `user-${customerExternalId}@example.com`,
                name: `User ${customerExternalId}`,
            }
        },
    })
}
