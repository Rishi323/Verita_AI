const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_API_KEY);

async function checkUser() {
    const { data: { session }, error } = await supabase.auth.getSession();
    
    if (!session) {
        // Redirect to login if not authenticated
        window.location.href = '/login';
    }
    return session;
}

// Add this to pages that require authentication
document.addEventListener('DOMContentLoaded', async () => {
    const session = await checkUser();
    if (!session) return;
    
    // Initialize your protected page content
    // For example, load user data or perform other authenticated actions
});

