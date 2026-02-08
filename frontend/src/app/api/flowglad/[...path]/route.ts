import { nextRouteHandler } from '@flowglad/nextjs/server'
import { flowglad } from '@/lib/flowglad'

/**
 * FlowGlad API route handler.
 * 
 * This catches all requests to /api/flowglad/* and delegates them to FlowGlad.
 * The getCustomerExternalId function extracts the user ID from the request.
 */
export const { GET, POST } = nextRouteHandler({
    flowglad,
    getCustomerExternalId: async (req) => {
        // TODO: Extract the real user ID from your auth/session system
        // Examples:
        //   - Next-Auth: const session = await getServerSession(); return session?.user?.id
        //   - Clerk: const { userId } = auth(); return userId
        //   - Custom JWT: const token = req.headers.get('authorization'); return decodeToken(token).userId

        // For now, use a default user ID for testing
        return 'default-user-id'
    },
})
