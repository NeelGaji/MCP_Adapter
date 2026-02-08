'use client'

import { useBilling } from '@flowglad/nextjs'
import { useState, useEffect } from 'react'

interface BillingButtonProps {
    priceSlug?: string
    className?: string
}

/**
 * Billing button component that shows upgrade option or pro badge.
 * 
 * IMPORTANT: This component requires products to be configured in FlowGlad dashboard.
 * Without products, the checkout will fail with a 500 error.
 * 
 * Visit /billing/debug to see your configuration status.
 */
export function BillingButton({
    priceSlug,
    className = ''
}: BillingButtonProps) {
    const {
        checkFeatureAccess,
        createCheckoutSession,
        loaded,
        errors,
        pricingModel,
    } = useBilling()
    const [isLoading, setIsLoading] = useState(false)
    const [debugInfo, setDebugInfo] = useState<string | null>(null)

    // Debug: Log pricing model when it changes
    useEffect(() => {
        if (loaded) {
            const products = pricingModel?.products || []
            const info = `Products: ${products.length}, Prices: ${products.flatMap(p => p.prices || []).length}`
            console.log('[FlowGlad BillingButton]', info, pricingModel)
            setDebugInfo(info)
        }
    }, [loaded, pricingModel])

    // Log any errors from the billing context
    if (errors?.length) {
        console.error('[FlowGlad] Billing errors:', errors)
    }

    if (!loaded) {
        return (
            <button
                disabled
                className={`opacity-50 cursor-not-allowed px-4 py-2 rounded-lg text-sm ${className}`}
            >
                Loading...
            </button>
        )
    }

    const hasPremium = checkFeatureAccess?.('premium_features')

    if (hasPremium) {
        return (
            <span className={`inline-flex items-center gap-1 px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm font-medium ${className}`}>
                Pro User ✓
            </span>
        )
    }

    // Get the first available price from pricing model if no priceSlug provided
    const products = pricingModel?.products || []
    const firstProduct = products[0]
    const firstPrice = firstProduct?.defaultPrice ?? firstProduct?.prices?.[0]
    const effectivePriceSlug = priceSlug || firstPrice?.slug

    // NO PRODUCTS CONFIGURED - Show helpful message instead of broken button
    if (products.length === 0 || !effectivePriceSlug) {
        return (
            <a
                href="https://app.flowglad.com"
                target="_blank"
                rel="noopener noreferrer"
                className={`inline-flex items-center gap-2 px-4 py-2 bg-yellow-500/20 text-yellow-400 font-medium rounded-lg border border-yellow-500/30 hover:bg-yellow-500/30 transition-colors ${className}`}
                title="Click to open FlowGlad dashboard and configure products"
            >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Setup Billing
            </a>
        )
    }

    const handleUpgrade = async () => {
        setIsLoading(true)

        try {
            console.log('[FlowGlad] Creating checkout with priceSlug:', effectivePriceSlug)

            await createCheckoutSession?.({
                priceSlug: effectivePriceSlug,
                successUrl: `${window.location.origin}/success`,
                cancelUrl: window.location.href,
                autoRedirect: true,
            })
        } catch (err) {
            console.error('[FlowGlad] Checkout failed:', err)
            alert('Checkout failed. Please check browser console for details.')
        } finally {
            setIsLoading(false)
        }
    }

    // Get price display info
    const priceDisplay = firstPrice
        ? `$${(firstPrice.unitAmount / 100).toFixed(0)}/${firstPrice.intervalUnit || 'mo'}`
        : ''

    return (
        <button
            onClick={handleUpgrade}
            disabled={isLoading}
            className={`px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 ${className}`}
        >
            {isLoading ? 'Processing...' : `Upgrade to Pro ${priceDisplay}`}
        </button>
    )
}
