import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import VerifyPage from "./pages/VerifyPage";
import ListingsPage from "./pages/ListingsPage";
import ProtectedRoute from "./components/common/ProtectedRoute";
import ListingDetailPage from "./pages/ListingDetailPage";
import CreateListingPage from "./pages/CreateListingPage";
import MyListingsPage from "./pages/MyListingsPage";
import FavoritesPage from "./pages/FavoritesPage";
import ProfilePage from "./pages/ProfilePage";
import EditProfilePage from "./pages/EditProfilePage";
import MessagesPage from "./pages/MessagesPage";
import EditListingPage from "./pages/EditListingPage";
import PaymentVerifyPage from "./pages/PaymentVerifyPage";
import PaymentHistoryPage from "./pages/PaymentHistoryPage";
import DealerApplicationPage from "./pages/DealerApplicationPage";
import PricingPage from "./pages/PricingPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Toaster position="top-right" />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/pricing" element={<PricingPage />} />
          <Route path="/listings" element={<ListingsPage />} />
          <Route path="/listings/:id" element={<ListingDetailPage />} />
          <Route
            path="/listings/create"
            element={
              <ProtectedRoute>
                <CreateListingPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/my-listings"
            element={
              <ProtectedRoute>
                <MyListingsPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/messages"
            element={
              <ProtectedRoute>
                <MessagesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/favorites"
            element={
              <ProtectedRoute>
                <FavoritesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile/edit"
            element={
              <ProtectedRoute>
                <EditProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/listings/:id/edit"
            element={
              <ProtectedRoute>
                <EditListingPage />
              </ProtectedRoute>
            }
          />

          {/* Payment Routes */}
          <Route
            path="/payment/verify"
            element={
              <ProtectedRoute>
                <PaymentVerifyPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/payments/history"
            element={
              <ProtectedRoute>
                <PaymentHistoryPage />
              </ProtectedRoute>
            }
          />

          {/* Dealer Application */}
          <Route
            path="/become-dealer"
            element={
              <ProtectedRoute>
                <DealerApplicationPage />
              </ProtectedRoute>
            }
          />

          {/* Protected Routes */}
          <Route
            path="/verify"
            element={
              <ProtectedRoute>
                <VerifyPage />
              </ProtectedRoute>
            }
          />

          {/* Catch all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
