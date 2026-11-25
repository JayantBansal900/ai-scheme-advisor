import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import App from "./App";

const searchBox = () => screen.getByPlaceholderText(/what are you looking for/i);
const searchButton = () => screen.getByRole("button", { name: "Search" });

const mockApi = (body, ok = true) => {
  global.fetch = jest.fn().mockResolvedValue({ ok, json: async () => body });
};

afterEach(() => {
  jest.restoreAllMocks();
  delete global.fetch;
});

test("renders the hero, search box and filters", () => {
  render(<App />);
  expect(screen.getByRole("heading", { name: /find the right government schemes/i })).toBeInTheDocument();
  expect(searchBox()).toBeInTheDocument();
  expect(screen.getByRole("option", { name: "Tamil Nadu" })).toBeInTheDocument();
  expect(screen.getByRole("option", { name: /all india/i })).toBeInTheDocument();
});

test("clicking a quick tag fills the search box", () => {
  render(<App />);
  fireEvent.click(screen.getByRole("button", { name: "#farmer" }));
  expect(searchBox()).toHaveValue("farmer");
});

test("does not call the API for an empty query", () => {
  mockApi({});
  render(<App />);
  fireEvent.click(searchButton());
  expect(global.fetch).not.toHaveBeenCalled();
});

test("sends the query and filters, then shows the AI pick and results", async () => {
  mockApi({
    predicted_scheme: "PM Scholarship Scheme",
    recommendations: [
      {
        scheme_name: "Post Matric Scholarship",
        state: "kerala",
        type: "state",
        eligibility: "Students from low-income families",
        benefits: "Tuition fee support",
        summary: "Covers tuition for higher studies",
      },
    ],
  });
  render(<App />);

  fireEvent.change(searchBox(), { target: { value: "scholarship" } });
  fireEvent.change(screen.getByDisplayValue("Categories"), { target: { value: "education" } });
  fireEvent.click(searchButton());

  expect(await screen.findByText("Post Matric Scholarship")).toBeInTheDocument();
  expect(screen.getByText("PM Scholarship Scheme")).toBeInTheDocument();
  expect(screen.getByText(/tuition fee support/i)).toBeInTheDocument();

  const [url, options] = global.fetch.mock.calls[0];
  expect(url).toMatch(/\/recommend$/);
  expect(JSON.parse(options.body)).toMatchObject({ query: "scholarship", category: "education" });
});

test("pressing Enter in the search box also searches", async () => {
  mockApi({ recommendations: [] });
  render(<App />);
  fireEvent.change(searchBox(), { target: { value: "health" } });
  fireEvent.keyDown(searchBox(), { key: "Enter" });
  await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(1));
});

test("shows no results when the API fails", async () => {
  jest.spyOn(console, "error").mockImplementation(() => {});
  mockApi({}, false);
  render(<App />);
  fireEvent.change(searchBox(), { target: { value: "startup" } });
  fireEvent.click(searchButton());

  await waitFor(() => expect(searchButton()).toBeEnabled());
  expect(screen.queryByText(/ai top pick/i)).not.toBeInTheDocument();
});
